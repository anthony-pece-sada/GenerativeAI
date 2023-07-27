question_prompt_template = """
                  Please provide a summary of the following text.
                  TEXT: {text}
                  SUMMARY:
                  """

refine_prompt_template = """
              Write a concise summary of the following text in 3-4 lines.
              Return your response in 3-4 lines of text which covers the key points of the text.
              ```{text}```
              BULLET POINT SUMMARY:
              """
