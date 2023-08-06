import argparse
import sys
from string_algorithms.trie import Trie
from collections import deque, Counter
import re
from itertools import islice


def build_trie(words):
    trie = Trie()

    for word in words:
        trie.add(word)

    return trie


def initialize_dictionary(dict_fname):
    print("Initializing dictionary...", file=sys.stderr)
    with open(dict_fname) as f:
        words = list(map(str.strip, f.readlines()))
    trie = build_trie(words)
    print("Done.", file=sys.stderr)
    return trie, words


def find_word(word, trie):
    return trie.find(word)


def find_subtree(word, trie, limit=None):
    root = trie.get_node(word)
    q = deque([(root, word)])
    words = []

    while len(q):
        node, w = q.popleft()
        if node.is_word:
            words.append(w)
        for c, subnode in sorted(node.children.items()):
            if limit is not None and limit > 0:
                if subnode.is_word:
                    words.append(w)
                    limit -= 1
                q.append((subnode, w + c))
    return words


def find_permutations(word, trie, use_all_letters=True, wildchar=None, limit=None):
    root = trie.root
    letters = Counter(word)
    q = deque([(root, "", letters)])
    words = []

    while len(q):
        node, w, l = q.popleft()

        if wildchar is None or l[wildchar] == 0:
            subnodes = sorted(
                filter(lambda item: l[item[0]] > 0, node.children.items())
            )
        else:
            subnodes = sorted(node.children.items())

        for c, subnode in subnodes:
            if limit is not None and limit > 0:
                new_w = w + c
                if (not use_all_letters or len(new_w) == len(word)) and subnode.is_word:
                    words.append(new_w)
                    limit -= 1
                new_l = l - Counter(c) if l[c] > 0 else l - Counter(wildchar)
                q.append((subnode, new_w, new_l))
    return words


def find_regex(regex, words, limit=None):
    pattern = re.compile(regex)
    words = filter(lambda w: pattern.match(w), words)
    if limit:
        return list(islice(words, limit))
    return list(words)


def _print_list(words):
    for word in words:
        print(word)


def answer(word, trie, words, args):
    if args.subtree:
        _print_list(find_subtree(word, trie, limit=args.limit))
    elif args.permutations:
        _print_list(
            find_permutations(
                word, trie, use_all_letters=not args.allow_shorter,
                wildchar=args.wildchar, limit=args.limit
            )
        )
    elif args.regex:
        _print_list(find_regex(word, words, limit=args.limit))
    else:
        print(find_word(word, trie))


def main():
    parser = argparse.ArgumentParser(description="Scrabbler")
    parser.add_argument("word", type=str, nargs='?', help="Input word")
    parser.add_argument("-d", "--dictionary", type=str, help="Dictironary to search.")
    parser.add_argument(
        "-l", "--limit", type=int, help="Limit the number of words printed"
    )
    parser.add_argument(
        "--subtree", action="store_true", help="Print all words starting by [word]"
    )
    parser.add_argument(
        "-p", "--permutations", action="store_true", help="Print all permutations"
    )
    parser.add_argument(
        "--allow_shorter", action="store_true", help="Don't require using all letters."
    )
    parser.add_argument(
        "--wildchar", action="store", const='?', nargs='?',
        help="Set a wildchar for the permutation matching (default: '?')"
    )
    parser.add_argument(
        "-r", "--regex", action="store_true", help="Print words matching regex."
    )

    args = parser.parse_args()

    trie, words = initialize_dictionary(args.dictionary)

    if args.word:
        answer(args.word, trie, words, args)
    else:
        while(word := input(">>> ")):
            answer(word, trie, words, args)


if __name__ == "__main__":
    main()
