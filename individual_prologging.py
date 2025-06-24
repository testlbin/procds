import pyswip
import argparse
import json

# def run_query(assert_path, mi_path, output_path, max_result=20):
#     """
#     Execute Prolog query with given parameters.
#
#     :param assert_path: Path to the file containing Prolog clauses to assert.
#     :param mi_path: Path to the file containing the Prolog knowledge base to consult.
#     :param output_path: Path where the output of the query will be saved.
#     :param max_result: Maximum number of results to return.
#     """
#     assert_path = assert_path.replace('\\', '\\\\')
#     mi_path = mi_path.replace('\\', '\\\\')
#     output_path = output_path.replace('\\', '\\\\')
#
#     prolog = pyswip.Prolog()
#
#     with open(assert_path, 'r', encoding='utf-8') as f:
#         _clauses = [_.strip() for _ in f.readlines() if _.strip()]
#     query = _clauses[-1]
#     clauses = _clauses[:-1]
#
#     query = query.rstrip('.')
#
#     try:
#         prolog.consult(mi_path)
#         for clause in clauses:
#             clause = clause.rstrip('.')
#             prolog.assertz(clause)
#         results = prolog.query(query, maxresult=max_result)
#
#
#
#
#         with open(output_path, 'w', encoding='utf-8') as f:
#             for r in results:
#                 f.write(json.dumps(r).strip() + '\n')
#     except pyswip.prolog.PrologError as e:
#         print(f"An error occurred: {e}")
#         return 1
#     return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--assert_path", type=str, required=True, help="")
    parser.add_argument("--mi_path", type=str, required=True, help="")
    parser.add_argument('--output_path', type=str, required=True)
    # parser.add_argument('--query', type=str, required=True)
    parser.add_argument("--max_result", type=int, default=20)

    args = parser.parse_args()

    prolog = pyswip.Prolog()

    with open(args.assert_path, 'r', encoding='utf-8') as f:
        _clauses = [_.strip() for _ in f.readlines() if _.strip()]
    query = _clauses[-1]
    clauses = _clauses[:-1]

    query = query.rstrip('.')

    try:
        prolog.consult(args.mi_path)
        for clause in clauses:
            clause = clause.rstrip('.')
            prolog.assertz(clause)

        results = prolog.query(query, maxresult=args.max_result)

        with open(args.output_path, 'w', encoding='utf-8') as f:
            for r in results:
                f.write(json.dumps(r).strip() + '\n')
    except pyswip.prolog.PrologError as e:
        pass