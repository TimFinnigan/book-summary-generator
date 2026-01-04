"""
Module for generating book summaries using OpenAI's GPT API.
Creates factual, neutral summaries to help readers refresh their memory.
Supports iterative refinement of summaries.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class SummaryGenerator:
    """Generates factual book summaries to refresh readers' memory of key events and concepts."""
    
    def __init__(self):
        """Initialize the OpenAI client."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = []
    
    def generate_summary(self, book_title, book_author=None, additional_context=None, 
                        summary_length="long", model="gpt-4o-mini"):
        """
        Generate a summary for a book.
        
        Args:
            book_title: Title of the book
            book_author: Author of the book (optional)
            additional_context: Any additional context or specific aspects to focus on
            summary_length: "short" (150-200 words), "medium" (300-400 words), "long" (600-800 words, default)
            model: OpenAI model to use
        
        Returns:
            Generated summary text
        """
        length_guidelines = {
            "short": "150-200 words, focusing on the most essential events and concepts",
            "medium": "300-400 words, covering key events, themes, and main points",
            "long": "600-800 words, providing comprehensive coverage with important details and context"
        }
        
        author_text = f" by {book_author}" if book_author else ""
        context_text = f"\n\nAdditional context: {additional_context}" if additional_context else ""
        
        prompt = f"""Create a factual summary of the book "{book_title}"{author_text}.

Length requirement: {length_guidelines.get(summary_length, length_guidelines["long"])}

IMPORTANT - Format for audio narration:
- Write in flowing, natural paragraphs that work well when read aloud
- Do NOT use bullet points, lists, headers, or any special formatting
- Structure the content as continuous prose with smooth transitions between ideas
- Use complete sentences and natural paragraph breaks

Content requirements:
- Provide a clear, neutral overview of the book's content
- Present key events, concepts, and important details in a straightforward manner
- Use factual language to help readers refresh their memory of what happened
- Include sufficient detail to capture the essential elements
- Progress logically through the material with clear narrative flow
- Avoid promotional language or subjective opinions{context_text}

Generate the summary as continuous prose:"""
        
        # Clear conversation history for new summary
        self.conversation_history = [
            {"role": "system", "content": "You are an expert book summarizer. Create clear, factual summaries that help readers refresh their memory of what happened in the book. Write in flowing paragraphs suitable for audio narration - no bullet points, lists, or headers. Use neutral, objective language and include key details, events, and main points."},
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
    
    # Generate initial summary (defaults to "long" for comprehensive detail)
    summary = generator.generate_summary(
        book_title="Atomic Habits",
        book_author="James Clear"
    )
    print("Generated Summary:")
    print(summary)
    print("\n" + "="*50 + "\n")
    
    # Refine the summary
    refined = generator.refine_summary("Make it more concise and focus on the core habit-building framework")
    print("Refined Summary:")
    print(refined)

