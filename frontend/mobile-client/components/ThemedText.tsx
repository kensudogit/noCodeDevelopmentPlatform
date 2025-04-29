// テキストコンポーネントとスタイルシートをインポート
import { Text, type TextProps, StyleSheet } from 'react-native';

// useThemeColorフックをインポート
import { useThemeColor } from '@/hooks/useThemeColor';

// ThemedTextコンポーネントは、テーマに応じた色を持つテキストを表示します。
// lightColorとdarkColorを指定することで、テーマに応じた色を設定できます。
// typeプロパティでテキストのスタイルを指定できます。

// ThemedTextコンポーネントのプロパティタイプを定義
export type ThemedTextProps = TextProps & {
  lightColor?: string;
  darkColor?: string;
  type?: 'default' | 'title' | 'defaultSemiBold' | 'subtitle' | 'link';
};

// ThemedTextコンポーネントを定義
export function ThemedText({
  style,
  lightColor,
  darkColor,
  type = 'default',
  ...rest
}: ThemedTextProps) {
  // テーマに基づいてテキストの色を取得
  const color = useThemeColor({ light: lightColor, dark: darkColor }, 'text');

  // スタイルを適用してTextコンポーネントを返す
  return (
    <Text
      style={[
        { color },
        type === 'default' ? styles.default : undefined,
        type === 'title' ? styles.title : undefined,
        type === 'defaultSemiBold' ? styles.defaultSemiBold : undefined,
        type === 'subtitle' ? styles.subtitle : undefined,
        type === 'link' ? styles.link : undefined,
        style,
      ]}
      {...rest}
    />
  );
}

// スタイルを定義
const styles = StyleSheet.create({
  default: {
    fontSize: 16,
    lineHeight: 24,
  },
  defaultSemiBold: {
    fontSize: 16,
    lineHeight: 24,
    fontWeight: '600',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    lineHeight: 32,
  },
  subtitle: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  link: {
    lineHeight: 30,
    fontSize: 16,
    color: '#0a7ea4',
  },
});
