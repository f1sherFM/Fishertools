"""Unified fishertools command-line interface."""

from __future__ import annotations

import json

import click

from fishertools.learn import explain, get_topic, search_topics
from fishertools.learn.repl.engine import REPLEngine
from fishertools.learning.models import DifficultyLevel
from fishertools.learning.tutorial import TutorialEngine


@click.group()
def main() -> None:
    """Fishertools CLI."""


@main.group()
def learn() -> None:
    """Learning flows: topic, quiz, explain, repl."""


@learn.command("topic")
@click.argument("topic")
def learn_topic(topic: str) -> None:
    """Show details for a learning topic."""
    data = get_topic(topic)
    if data is None:
        matches = search_topics(topic)
        if matches:
            data = get_topic(matches[0])
    if data is None:
        raise click.ClickException(f"Topic not found: {topic}")
    click.echo(json.dumps(data, ensure_ascii=False, indent=2))


@learn.command("explain")
@click.argument("topic")
def learn_explain(topic: str) -> None:
    """Explain a topic."""
    click.echo(explain(topic))


@learn.command("quiz")
@click.argument("topic")
@click.option(
    "--level",
    type=click.Choice(["beginner", "intermediate", "advanced"]),
    default="beginner",
    show_default=True,
)
def learn_quiz(topic: str, level: str) -> None:
    """Generate a quick exercise for a topic."""
    engine = TutorialEngine()
    exercise = engine.create_interactive_exercise(topic, DifficultyLevel(level))

    click.echo(f"Quiz: {exercise.title}")
    click.echo(exercise.description)
    click.echo("\nStarter code:")
    click.echo(exercise.starter_code)
    if exercise.hints:
        click.echo("Hint: " + exercise.hints[0])


@learn.command("repl")
def learn_repl() -> None:
    """Run interactive REPL learning session."""
    REPLEngine().start()


if __name__ == "__main__":
    main()
