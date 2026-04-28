from backend.rag.prompt import PROMPT_TEMPLATE, build_prompt


def test_build_prompt_uses_exact_template():
    prompt = build_prompt(context="Policy context", question="What is the policy?")

    assert prompt == PROMPT_TEMPLATE.format(
        context="Policy context",
        question="What is the policy?",
    )
    assert 'say "I don\'t know"' in prompt
    assert prompt.endswith("Answer:")
