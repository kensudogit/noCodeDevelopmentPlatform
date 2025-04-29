// frontend/src/Items.tsx
import React from 'react';
import { ApolloClient, InMemoryCache, useSubscription, gql, split, HttpLink } from '@apollo/client';
import { WebSocketLink } from '@apollo/client/link/ws';
import { getMainDefinition } from '@apollo/client/utilities';

const httpLink = new HttpLink({
  uri: 'http://localhost:8000/graphql',
});

const wsLink = new WebSocketLink({
  uri: 'ws://localhost:8000/graphql',
  options: {
    reconnect: true
  }
});

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

const client = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache()
});

// サブスクリプション
const ITEM_ADDED_SUBSCRIPTION = gql`
  subscription {
    onItemAdded {
      id
      data
    }
  }
`;

// 画面コンポーネント
export function Items() {
  const { data, loading } = useSubscription(ITEM_ADDED_SUBSCRIPTION);

  if (loading) return <p>Waiting for updates...</p>;

  return (
    <div>
      <h2>New Item Added!</h2>
      <p>ID: {data?.onItemAdded.id}</p>
      <p>Data: {data?.onItemAdded.data}</p>
    </div>
  );
}

// index.tsxでApolloProviderにclient渡すのを忘れずに！
