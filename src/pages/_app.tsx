import React from 'react';
import '@aws-amplify/ui-react/styles.css';
import { Amplify } from 'aws-amplify';
import awsconfig from '../aws-exports';
import type { AppProps } from 'next/app';
import { Authenticator } from '@aws-amplify/ui-react';

Amplify.configure({
  ...(awsconfig as any),
  ssr: true
});

export default function App({ Component, pageProps }: AppProps) {
  return (
    <Authenticator>
      <Component {...pageProps} />
    </Authenticator>
  );
}