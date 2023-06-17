import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

const InnerRing = ({
  radius,
  tube,
  position,
  rotationSpeed,
  glowIntensity,
}) => {
  const ringRef = useRef();
  const leftRingRef = useRef();
  const rightRingRef = useRef();
  const innerRingRef = useRef();

  useFrame((state, delta) => {
    ringRef.current && (ringRef.current.rotation.z += delta * rotationSpeed);
    leftRingRef.current &&
      (leftRingRef.current.rotation.z += delta * rotationSpeed);
    rightRingRef.current &&
      (rightRingRef.current.rotation.z += delta * rotationSpeed);
    innerRingRef.current &&
      (innerRingRef.current.rotation.z += delta * -rotationSpeed);
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

  const innerGeometry = useMemo(
    () =>
      new THREE.RingGeometry(
        radius - 7 * tube,
        radius - 6 * tube,
        2000,
        1,
        0,
        Math.PI * 1.25
      ),
    [radius, tube]
  );

  const material = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: "#7B0090",
        emissive: "#7B0090",
        emissiveIntensity: glowIntensity / 2,
        flatShading: true,
        side: THREE.DoubleSide,
      }),
    [glowIntensity]
  );

  const innerMaterial = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: "#9EF4FF",
        emissive: "#9EF4FF",
        emissiveIntensity: glowIntensity,
        flatShading: true,
        side: THREE.DoubleSide,
      }),
    [glowIntensity]
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
      <mesh
        geometry={innerGeometry}
        material={innerMaterial}
        position={position}
        ref={innerRingRef}
      />
    </>
  );
};

export default InnerRing;
