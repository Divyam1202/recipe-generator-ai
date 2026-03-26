import unittest

from backend.app.prompt_builder import build_generation_context, normalize_conversation, should_enforce_recipe_format
from backend.app.schemas import MessageModel


class PromptBuilderTests(unittest.TestCase):
    def test_follow_up_summary_does_not_require_recipe_format(self):
        messages = [
            MessageModel(id=1, type="user", content="tomato pasta"),
            MessageModel(id=2, type="ai", content="A complete recipe response"),
            MessageModel(id=3, type="user", content="Summarize this"),
        ]

        context = build_generation_context("Summarize this", messages)

        self.assertFalse(context["require_recipe"])

    def test_first_turn_defaults_to_recipe_mode(self):
        messages = [MessageModel(id=1, type="user", content="paneer, corn, capsicum under 400 calories")]

        context = build_generation_context(messages[0].content, messages)

        self.assertTrue(context["require_recipe"])

    def test_prompt_echo_and_error_messages_are_removed_from_context(self):
        messages = [
            MessageModel(id=1, type="user", content="ingredients"),
            MessageModel(id=2, type="ai", content="You are an expert professional chef. Create a COMPLETE and DETAILED recipe"),
            MessageModel(id=3, type="ai", content="Error: Failed to generate recipe"),
            MessageModel(id=4, type="user", content="Summarize this"),
        ]

        normalized = normalize_conversation(messages)

        self.assertEqual(normalized, [{"role": "user", "content": "ingredients"}, {"role": "user", "content": "Summarize this"}])

    def test_explicit_recipe_follow_up_stays_in_recipe_mode(self):
        normalized = [
            {"role": "user", "content": "first request"},
            {"role": "assistant", "content": "first reply"},
            {"role": "user", "content": "Give me another recipe with paneer and corn"},
        ]

        self.assertTrue(should_enforce_recipe_format("Give me another recipe with paneer and corn", normalized))


if __name__ == "__main__":
    unittest.main()
