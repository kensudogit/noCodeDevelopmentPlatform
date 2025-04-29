import { meshStandardMaterial, boxGeometry } from '@react-three/fiber';

export function BuildingBasic() {
  return (
    <mesh position={[0, 0, 0]}>
      <boxGeometry args={[2, 6, 2]} />
      <meshStandardMaterial color="gray" />
    </mesh>
  );
}
