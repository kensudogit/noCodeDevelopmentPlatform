import React from 'react';
import { Canvas } from '@react-three/fiber';

export function TreeSimple() {
  return (
    <Canvas>
      <mesh position={[0, 0, 0]}>
        <cylinderGeometry args={[0.5, 0.5, 2]} />
        <meshStandardMaterial color="brown" />
      </mesh>
      <mesh position={[0, 1.5, 0]}>
        <coneGeometry args={[1.5, 3, 8]} />
        <meshStandardMaterial color="green" />
      </mesh>
    </Canvas>
  );
}
