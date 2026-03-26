import unittest

from backend.app.recipe_utils import strip_prompt_echo, validate_recipe_structure


class RecipeUtilsTests(unittest.TestCase):
    def test_strip_prompt_echo_removes_prefixed_prompt_and_marker(self):
        prompt = "You are a chef.\nNow write the complete detailed recipe with ALL sections:"
        generated = (
            "You are a chef.\nNow write the complete detailed recipe with ALL sections:\n"
            "Sunlit Pasta\nPrep Time - 10 minutes\nCook Time - 20 minutes\nServings - 2\n"
        )

        cleaned = strip_prompt_echo(prompt, generated)

        self.assertEqual(
            cleaned,
            "Sunlit Pasta\nPrep Time - 10 minutes\nCook Time - 20 minutes\nServings - 2",
        )

    def test_validate_recipe_structure_accepts_well_formed_recipe(self):
        recipe = """
Lemon Herb Pasta

Prep Time - 10 minutes
Cook Time - 20 minutes
Servings - 2

Ingredients
- 200 g pasta
- 30 ml olive oil

Instructions
1. Boil the pasta until tender.
2. Toss it with olive oil and herbs.

Serving Tips
- Garnish with parsley.
- Store leftovers in the fridge.
""".strip()

        self.assertTrue(validate_recipe_structure(recipe))

    def test_validate_recipe_structure_rejects_missing_sections(self):
        recipe = "Ingredients\n- pasta\n- salt\n"

        self.assertFalse(validate_recipe_structure(recipe))


if __name__ == "__main__":
    unittest.main()
