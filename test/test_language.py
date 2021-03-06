#!/usr/bin/env python

import networkx

import pytest

from phylo.language import Language


@pytest.fixture
def language():
    return Language({"a": ["b", "c"],
                     "b": ["a"],
                     "c": ["b"]})


@pytest.fixture
def specific_language():
    l = Language({})
    l._cum_concept_weights = [1, 2]
    l._word_meaning_pairs = [(0, "a"),
                             (1, "a")]
    l.related_concepts = {"a": ["b"], "b": ["b"]}
    return l


@pytest.fixture
def specific_language():
    l = Language({})
    l._cum_concept_weights = [1, 2]
    l._word_meaning_pairs = [(0, "a"),
                             (1, "a")]
    l.related_concepts = networkx.Graph()
    l.related_concepts.add_edges_from([("a", "b"), ("b", "b")])
    return l


def test_clone():
    l = language()
    m = l.clone()
    assert l.flat_frequencies() == m.flat_frequencies()
    m.loss()
    assert l.flat_frequencies() != m.flat_frequencies()


def test_add_link():
    l = language()
    old_signs = l._word_meaning_pairs[:]
    l.new_word()
    new_signs = l._word_meaning_pairs[:]
    assert len(old_signs) + 1 == len(new_signs)


def test_gain():
    l = language()
    old_weights = l._cum_concept_weights[-1]
    l.gain()
    new_weights = l._cum_concept_weights[-1]
    assert (old_weights) + 1 == (new_weights)


def test_gain_new_concept():
    l = specific_language()
    l.gain()
    assert (
        (0, "b") in l._word_meaning_pairs or
        (1, "b") in l._word_meaning_pairs)


def test_loss():
    l = language()
    old_weights = sum(l.flat_frequencies().values())
    l.loss()
    assert (old_weights) - 1 == sum(l.flat_frequencies().values())


def test_words_for_concept():
    l = specific_language()
    assert set(l.words_for_concept("a")) == {0, 1}
