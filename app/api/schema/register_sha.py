def reg_args_valid(parser):
    parser.add_argument('username', type=str, location='json')
    parser.add_argument('password', type=str, dest='password', location='json')