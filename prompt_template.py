def build_prompt(language: str, cwe: str, code: str, context: str = None) -> str:
    """Builds the prompt for the LLM."""
    
    prompt = f"""You are an expert secure code reviewer.
Your task is to fix the following {language} code which has a {cwe} vulnerability.

"""
    if context:
        prompt += f"""Here is some context and guidance on how to fix this issue:
{context}

"""

    prompt += f"""Please provide the fixed code, a unified diff, and an explanation.
Strictly follow this output format:

---FIXED_CODE---
<put the fixed code here>

---DIFF---
<put the unified diff here>

---EXPLANATION---
<put the explanation here>

Vulnerable Code:
```{language}
{code}
```

Response:
"""
    return prompt
