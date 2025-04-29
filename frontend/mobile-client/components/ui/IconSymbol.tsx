// このファイルは、AndroidとWebでMaterialIconsを使用するためのフォールバックです。

import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import { SymbolWeight } from 'expo-symbols';
import React from 'react';
import { OpaqueColorValue, StyleProp, ViewStyle } from 'react-native';

// MaterialIconsとSFSymbolsのマッピングをここに追加します。
// MaterialIconsの詳細はこちら: https://icons.expo.fyi
// SF Symbolsの詳細はMacのSF Symbolsアプリで確認できます。

// Add your SFSymbol to MaterialIcons mappings here.
const MAPPING = {
  // See MaterialIcons here: https://icons.expo.fyi
  // See SF Symbols in the SF Symbols app on Mac.
  'house.fill': 'home',
  'paperplane.fill': 'send',
  'chevron.left.forwardslash.chevron.right': 'code',
  'chevron.right': 'chevron-right',
} as Partial<
  Record<
    import('expo-symbols').SymbolViewProps['name'],
    React.ComponentProps<typeof MaterialIcons>['name']
  >
>;

export type IconSymbolName = keyof typeof MAPPING;

/**
 * iOSではネイティブのSFSymbolsを使用し、AndroidとWebではMaterialIconsを使用するアイコンコンポーネントです。
 * これにより、プラットフォーム間で一貫した外観と最適なリソース使用が保証されます。
 * アイコンの`name`はSFSymbolsに基づいており、MaterialIconsへの手動マッピングが必要です。
 */
export function IconSymbol({
  name,
  size = 24,
  color,
  style,
}: {
  name: IconSymbolName;
  size?: number;
  color: string | OpaqueColorValue;
  style?: StyleProp<ViewStyle>;
  weight?: SymbolWeight;
}) {
  return <MaterialIcons color={color} size={size} name={MAPPING[name]} style={style} />;
}
