"""
AI Content Generator using OpenAI
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Only create client if API key exists
api_key = os.getenv('OPENAI_API_KEY')
if api_key and not api_key.startswith('sk-your'):
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
else:
    client = None


class AIContentGenerator:
    def __init__(self):
        self.templates = {
            'blog_intro': "Write an engaging blog post introduction about: {prompt}. Make it attention-grabbing and SEO-friendly.",
            'blog_post': "Write a complete blog post (800-1000 words) about: {prompt}. Include introduction, main points, and conclusion. Make it SEO-optimized.",
            'social_post': "Write 3 engaging social media posts about: {prompt}. Make them catchy and shareable.",
            'email': "Write a professional email about: {prompt}. Make it clear, concise, and action-oriented.",
            'ad_copy': "Write compelling ad copy for: {prompt}. Include headline and body text. Focus on benefits and call-to-action.",
            'product_description': "Write a persuasive product description for: {prompt}. Highlight features and benefits.",
            'seo_meta': "Write SEO meta description (150-160 characters) for: {prompt}",
            'linkedin_post': "Write a professional LinkedIn post about: {prompt}. Make it insightful and engaging.",
            'tweet': "Write 5 engaging tweets about: {prompt}. Keep each under 280 characters.",
            'video_script': "Write a video script about: {prompt}. Include intro, main content, and outro."
        }

    def generate(self, content_type, prompt, plan='free'):
        """Generate AI content"""
        if not client:
            return f"Demo content: This is where AI-generated content would appear for '{prompt}'.\n\nTo enable real AI generation:\n1. Get an API key from https://platform.openai.com/api-keys\n2. Add it to your .env file: OPENAI_API_KEY=sk-your-key\n3. Restart the application\n\nThis demo content is just a placeholder. With a real OpenAI API key, you would get high-quality, AI-generated content based on your prompt."

        # Get template
        template = self.templates.get(content_type, "Write about: {prompt}")
        full_prompt = template.format(prompt=prompt)

        # Model selection based on plan
        model = 'gpt-4' if plan in ['pro', 'business'] else 'gpt-3.5-turbo'

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a professional content writer. Create high-quality, engaging content."},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=1500 if plan in ['pro', 'business'] else 500,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error generating content: {e}")
            return f"Error generating content. Please check your OpenAI API key and try again. Error: {str(e)}"

    def get_content_types(self):
        """Get available content types"""
        return list(self.templates.keys())
