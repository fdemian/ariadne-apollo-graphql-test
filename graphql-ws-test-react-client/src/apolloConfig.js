import { ApolloClient, InMemoryCache, split } from '@apollo/client';
import { createUploadLink } from 'apollo-upload-client';
import { getMainDefinition } from '@apollo/client/utilities'
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { createClient } from 'graphql-ws';

const httpLink = createUploadLink({ uri: '/api/graphql' });
const wsLink = new GraphQLWsLink(
  createClient({ url: 'ws://localhost:8000/api/subscriptions' })
);

const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === 'OperationDefinition' &&
      definition.operation === 'subscription'
    );
  },
  wsLink,
  httpLink
);

export const useNewClient = () => {
  return new ApolloClient({
    link: splitLink,
    cache: new InMemoryCache()
  });
};
