// frontend/src/App.tsx
import React from 'react';
import { ApolloClient, InMemoryCache, ApolloProvider, useQuery, gql } from '@apollo/client';

const client = new ApolloClient({
  uri: 'http://localhost:8000/graphql',
  cache: new InMemoryCache()
});

const HELLO_QUERY = gql`
  query SayHello($name: String) {
    hello(name: $name)
  }
`;

function Hello() {
  const { data, loading, error } = useQuery(HELLO_QUERY, {
    variables: { name: "Kenichi" }
  });

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  return <h1>{data.hello}</h1>;
}

function App() {
  return (
    <ApolloProvider client={client}>
      <Hello />
    </ApolloProvider>
  );
}

export default App;
