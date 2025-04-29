// expo-symbolsからSymbolView、SymbolViewProps、SymbolWeightをインポート
// react-nativeからStyleProp、ViewStyleをインポート
import { SymbolView, SymbolViewProps, SymbolWeight } from 'expo-symbols';
import { StyleProp, ViewStyle } from 'react-native';

// IconSymbolコンポーネントの定義
// name: シンボルの名前
// size: シンボルのサイズ（デフォルトは24）
// color: シンボルの色
// style: スタイルのオプション
// weight: シンボルの太さ（デフォルトは'regular'）
export function IconSymbol({
  name,
  size = 24,
  color,
  style,
  weight = 'regular',
}: Readonly<{
  name: SymbolViewProps['name'];
  size?: number;
  color: string;
  style?: StyleProp<ViewStyle>;
  weight?: SymbolWeight;
}>) {
  // SymbolViewコンポーネントを返す
  // weight: シンボルの太さ
  // tintColor: シンボルの色
  // resizeMode: シンボルのリサイズモード
  // name: シンボルの名前
  // style: スタイルの配列（サイズと追加スタイル）
  return (
    <SymbolView
      weight={weight}
      tintColor={color}
      resizeMode="scaleAspectFit"
      name={name}
      style={[
        {
          width: size,
          height: size,
        },
        style,
      ]}
    />
  );
}
