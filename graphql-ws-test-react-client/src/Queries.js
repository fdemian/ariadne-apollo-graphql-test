import { gql } from '@apollo/client';

export const GET_UNUSED = gql`
  query GetUnused {
    _unused
  }
`;
