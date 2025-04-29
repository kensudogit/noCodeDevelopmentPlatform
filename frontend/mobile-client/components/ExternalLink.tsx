// expo-routerからLinkコンポーネントをインポート
import { Link } from 'expo-router';
// expo-web-browserからopenBrowserAsyncをインポート
import { openBrowserAsync } from 'expo-web-browser';
// reactのComponentProps型をインポート
import { type ComponentProps } from 'react';
// react-nativeからPlatformをインポート
import { Platform } from 'react-native';

// LinkコンポーネントのComponentProps型から'href'を除外した型に、hrefプロパティを追加したProps型を定義
type Props = Omit<ComponentProps<typeof Link>, 'href'> & { href: string };

// ExternalLinkコンポーネントを定義
export function ExternalLink({ href, ...rest }: Props) {
  return (
    <Link
      target="_blank"
      {...rest}
      href={href}
      onPress={async (event) => {
        if (Platform.OS !== 'web') {
          // デフォルトのブラウザでリンクを開く動作を防ぐ
          event.preventDefault();
          // アプリ内ブラウザでリンクを開く
          await openBrowserAsync(href);
        }
      }}
    />
  );
}
