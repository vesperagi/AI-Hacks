import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

const CenterRing = ({
  radius,
  tube,
  position,
  rotationSpeed,
  glowIntensity,
}) => {
  const firstRingRef = useRef();
  const secondRingRef = useRef();
  const thirdRingRef = useRef();

  useFrame((state, delta) => {
    firstRingRef.current &&
      (firstRingRef.current.rotation.z += delta * -rotationSpeed);
    secondRingRef.current &&
      (secondRingRef.current.rotation.z += delta * rotationSpeed);
    thirdRingRef.current &&
      (thirdRingRef.current.rotation.z += delta * -rotationSpeed);
  });

  const firstGeometry = useMemo(
    () =>
      new THREE.RingGeometry(
        radius - tube,
        radius,
        2000,
        1,
        2 * Math.PI,
        Math.PI
      ),
    [radius, tube]
  );

  const secondGeometry = useMemo(
    () =>
      new THREE.RingGeometry(
        radius - 10 * tube,
        radius - 9 * tube,
        2000,
        1,
        (2 * Math.PI) / 3,
        Math.PI
      ),
    [radius, tube]
  );

  const thirdGeometry = useMemo(
    () =>
      new THREE.RingGeometry(
        radius - 20 * tube,
        radius - 19 * tube,
        2000,
        1,
        2 * ((2 * Math.PI) / 3),
        Math.PI
      ),
    [radius, tube]
  );

  const material = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: "#00FFFF",
        emissive: "#00FFFF",
        emissiveIntensity: glowIntensity,
        flatShading: true,
        side: THREE.DoubleSide,
      }),
    [glowIntensity]
  );

  return (
    <>
      <mesh
        geometry={firstGeometry}
        material={material}
        position={position}
        ref={firstRingRef}
      />
      <mesh
        geometry={secondGeometry}
        material={material}
        position={position}
        ref={secondRingRef}
      />
      <mesh
        geometry={thirdGeometry}
        material={material}
        position={position}
        ref={thirdRingRef}
      />
    </>
  );
};

export default CenterRing;
