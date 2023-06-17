import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

const OuterRing = ({
  radius,
  tube,
  position,
  rotationSpeed,
  glowIntensity,
}) => {
  const ringRef = useRef();
  const numberOfTicks = 36;
  const refs = Array.from({ length: numberOfTicks }, () => useRef());

  useFrame((state, delta) => {
    ringRef.current && (ringRef.current.rotation.z += delta * rotationSpeed);

    refs.forEach((ref) => {
      ref.current && (ref.current.rotation.z += delta * rotationSpeed);
    });
  });

  const geometry = useMemo(
    () =>
      new THREE.RingGeometry(radius - tube, radius, 2000, 1, 0, 2 * Math.PI),
    [radius, tube]
  );

  const geometries = refs.map((ref, index) => {
    return useMemo(() => {
      const angleBetweenTicks = (2 * Math.PI) / numberOfTicks;
      const tickAngle = index * angleBetweenTicks;

      const innerRadius = radius - 25 * tube;
      const outerRadius = radius - 5 * tube;

      const geometry = new THREE.RingGeometry(
        innerRadius,
        outerRadius,
        1,
        1,
        tickAngle,
        Math.PI / (numberOfTicks * 20)
      );

      return geometry;
    }, [radius, tube, index, numberOfTicks]);
  });

  const material = useMemo(
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
      {refs.map((ref, index) => (
        <mesh
          key={index}
          geometry={geometries[index]}
          material={material}
          position={position}
          ref={ref}
        />
      ))}
    </>
  );
};

export default OuterRing;
