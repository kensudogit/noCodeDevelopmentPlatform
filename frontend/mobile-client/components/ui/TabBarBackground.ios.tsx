// @react-navigation/bottom-tabsからuseBottomTabBarHeightをインポート
import { useBottomTabBarHeight } from '@react-navigation/bottom-tabs';
// expo-blurからBlurViewをインポート
import { BlurView } from 'expo-blur';
// react-nativeからStyleSheetをインポート
import { StyleSheet } from 'react-native';
// react-native-safe-area-contextからuseSafeAreaInsetsをインポート
import { useSafeAreaInsets } from 'react-native-safe-area-context';

// BlurTabBarBackgroundコンポーネントをエクスポート
export default function BlurTabBarBackground() {
  return (
    <BlurView
      // iOSでネイティブのタブバーの外観に合わせてシステムのテーマに自動適応するシステムクロームマテリアル
      // tintプロパティはシステムクロームマテリアルを指定
      tint="systemChromeMaterial"
      // intensityプロパティは100に設定
      intensity={100}
      // styleプロパティはStyleSheet.absoluteFillを指定
      style={StyleSheet.absoluteFill}
    />
  );
}

// useBottomTabOverflowフックをエクスポート
export function useBottomTabOverflow() {
  // タブの高さを取得
  const tabHeight = useBottomTabBarHeight();
  // セーフエリアの下部を取得
  const { bottom } = useSafeAreaInsets();
  // タブの高さからセーフエリアの下部を引いた値を返す
  return tabHeight - bottom;
}
