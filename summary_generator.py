"""
Module for generating book summaries using OpenAI's GPT API.
Supports iterative refinement of summaries.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class SummaryGenerator:
    """Handles book summary generation with OpenAI API."""
    
    def __init__(self):
        """Initialize the OpenAI client."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = []
    
    def generate_summary(self, book_title, book_author=None, additional_context=None, 
                        summary_length="medium", model="gpt-4o-mini"):
        """
        Generate a summary for a book.
        
        Args:
            book_title: Title of the book
            book_author: Author of the book (optional)
            additional_context: Any additional context or specific aspects to focus on
            summary_length: "short" (100-150 words), "medium" (250-350 words), "long" (500-700 words)
            model: OpenAI model to use
        
        Returns:
            Generated summary text
        """
        length_guidelines = {
            "short": "100-150 words, focusing on the core message only",
            "medium": "250-350 words, covering main themes and key insights",
            "long": "500-700 words, providing comprehensive coverage of major concepts and takeaways"
        }
        
        author_text = f" by {book_author}" if book_author else ""
        context_text = f"\n\nAdditional context: {additional_context}" if additional_context else ""
        
        prompt = f"""Create an engaging and insightful summary of the book "{book_title}"{author_text}.

Length requirement: {length_guidelines.get(summary_length, length_guidelines["medium"])}

The summary should:
- Capture the book's main themes and key ideas
- Be written in an engaging, conversational tone suitable for audio narration
- Avoid spoilers for fiction, focus on insights for non-fiction
- Be structured with clear flow from introduction to conclusion{context_text}

Generate the summary:"""
        
        # Clear conversation history for new summary
        self.conversation_history = [
            {"role": "system", "content": "You are an expert book reviewer and summarizer. Create summaries that are engaging, insightful, and well-structured."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.chat.completions.create(
            model=model,
            messages=self.conversation_history,
            temperature=0.7,
            max_tokens=1500
        )
        
        summary = response.choices[0].message.content
        
        # Add assistant response to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": summary
        })
        
        return summary
    
    def refine_summary(self, refinement_request, model="gpt-4o-mini"):
        """
        Refine the previously generated summary based on user feedback.
        
        Args:
            refinement_request: User's request for changes (e.g., "make it shorter", 
                              "focus more on the main character", "add more about the themes")
            model: OpenAI model to use
        
        Returns:
            Refined summary text
        """
        if not self.conversation_history:
            raise ValueError("No summary has been generated yet. Generate a summary first.")
        
        # Add user's refinement request to conversation
        self.conversation_history.append({
            "role": "user",
            "content": refinement_request
        })
        
        response = self.client.chat.completions.create(
            model=model,
            messages=self.conversation_history,
            temperature=0.7,
            max_tokens=1500
        )
        
        refined_summary = response.choices[0].message.content
        
        # Add assistant response to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": refined_summary
        })
        
        return refined_summary
    
    def reset(self):
        """Reset the conversation history."""
        self.conversation_history = []


if __name__ == "__main__":
    # Example usage
    generator = SummaryGenerator()
    
    # Generate initial summary
    summary = generator.generate_summary(
        book_title="Atomic Habits",
        book_author="James Clear",
        summary_length="medium"
    )
    print("Generated Summary:")
    print(summary)
    print("\n" + "="*50 + "\n")
    
    # Refine the summary
    refined = generator.refine_summary("Make it more concise and focus on the core habit-building framework")
    print("Refined Summary:")
    print(refined)

