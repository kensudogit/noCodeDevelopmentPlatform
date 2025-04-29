// @react-navigation/bottom-tabsからBottomTabBarButtonPropsをインポート
// @react-navigation/elementsからPlatformPressableをインポート
// expo-hapticsからHapticsをインポート
import { BottomTabBarButtonProps } from '@react-navigation/bottom-tabs';
import { PlatformPressable } from '@react-navigation/elements';
import * as Haptics from 'expo-haptics';

// HapticTabコンポーネントを定義
// BottomTabBarButtonPropsを受け取る
export function HapticTab(props: BottomTabBarButtonProps) {
  return (
    // PlatformPressableコンポーネントを返す
    // プロパティを展開して渡す
    <PlatformPressable
      {...props}
      // タブを押し込んだときに発生するイベント
      onPressIn={(ev) => {
        if (process.env.EXPO_OS === 'ios') {
          // iOSの場合、タブを押し込むときにソフトな触覚フィードバックを追加
          // Haptics.impactAsyncを使用して、軽い触覚フィードバックスタイルを指定
          Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
        }
        // onPressInプロパティが存在する場合、イベントを呼び出す
        props.onPressIn?.(ev);
      }}
    />
  );
}
