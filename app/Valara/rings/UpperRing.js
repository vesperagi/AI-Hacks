import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

const UpperRing = ({
  radius,
  tube,
  position,
  rotationSpeed,
  glowIntensity,
  targetRotation,
}) => {
  const ringRef = useRef();
  const leftRingRef = useRef();
  const rightRingRef = useRef();

  useFrame((state, delta) => {
    ringRef.current.rotation.z += delta * rotationSpeed;
    leftRingRef.current.rotation.z += delta * rotationSpeed;
    rightRingRef.current.rotation.z += delta * rotationSpeed;
  });

  const geometry = useMemo(
    () =>
      new THREE.RingGeometry(radius - tube, radius, 2000, 1, 0, 2 * Math.PI),
    [radius, tube]
  );

  const leftGeometry = useMemo(
    () =>
      new THREE.RingGeometry(
        radius,
        radius + tube,
        2000,
        1,
        Math.PI,
        Math.PI / 2
      ),
    [radius, tube]
  );

  const rightGeometry = useMemo(
    () =>
      new THREE.RingGeometry(radius, radius + tube, 2000, 1, 0, Math.PI / 2),
    [radius, tube]
  );

  const material = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: "#65EEFF",
        emissive: "#65EEFF",
        emissiveIntensity: 0,
        flatShading: true,
        side: THREE.DoubleSide,
      }),
    [0]
  );

  return (
    <>
      <mesh
        geometry={geometry}
        material={material}
        position={position}
        ref={ringRef}
      />
      <mesh
        geometry={leftGeometry}
        material={material}
        position={position}
        ref={leftRingRef}
      />
      <mesh
        geometry={rightGeometry}
        material={material}
        position={position}
        ref={rightRingRef}
      />
    </>
  );
};

export default UpperRing;
