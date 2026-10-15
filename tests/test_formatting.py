from industry_tycoon.formatting import money


def test_money_groups_thousands_and_rounds():
    assert money(1500) == "＄1,500"
    assert money(33.6) == "＄34"


def test_money_never_emits_markdown_math_delimiters():
    # Streamlit renders text between two ASCII "$" signs as LaTeX.
    assert "$" not in f"需要 {money(2400)}，目前只有 {money(1500)}"
