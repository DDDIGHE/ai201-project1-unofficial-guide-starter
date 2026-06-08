import sys

from query import ask


def main():
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        question = input("Question: ").strip()

    result = ask(question)
    print("\nAnswer\n------")
    print(result["answer"])
    print("\nSources\n-------")
    for source in result["sources"]:
        print(f"- {source}")
    print("\nRetrieved chunks\n----------------")
    for chunk in result["chunks"]:
        print(f"- {chunk['source']}#{chunk['chunk_index']} distance={chunk['distance']:.3f}")


if __name__ == "__main__":
    main()
