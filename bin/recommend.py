import os
from amis import reconstruct_multi_models

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='Recommend substitutions to a wildtype sequence'
    )
    parser.add_argument('sequence', type=str,
                        help='Wildtype sequence')
    parser.add_argument(
        '--model-names',
        type=str,
        default=[ 'esm1b', 'esm1v1', 'esm1v2', 'esm1v3', 'esm1v4', 'esm1v5', 'esm2_t36', 'esm2_t48', 'esm2_t33', 'esm2_t30', 'esm2_t12', 'esm2_t6'],
        nargs='+',
        help='Type of language model (e.g., esm1b, esm1v1)'
    )
    parser.add_argument(
        '--alpha',
        type=float,
        default=None,
        help='alpha stringency parameter'
    )
    parser.add_argument(
        '--cuda',
        type=str,
        default='cuda',
        help='cuda device to use'
    )
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()

    if ":" in args.cuda:
        os.environ["CUDA_VISIBLE_DEVICES"] = args.cuda.split(':')[-1]

    mutations_models = reconstruct_multi_models(
        args.sequence,
        args.model_names,
        alpha=args.alpha,
    )
    for k, v in sorted(mutations_models.items(), key=lambda item: -item[1]):
        mut_str = f'{k[0]}-{k[1]}:{k[3]}{k[2] + 1}{k[4]}'
        print(f'{mut_str}\t{v}')
