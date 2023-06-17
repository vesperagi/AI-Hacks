import { useRef, useState, useMemo, useEffect } from "react";

import { Box } from "@chakra-ui/react";

import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, useTexture } from "@react-three/drei";
import { ShaderMaterial } from "three";
import * as THREE from "three";

import UpperRing from "./rings/UpperRing";
import OuterRing from "./rings/OuterRing";
import InnerRing from "./rings/InnerRing";
import CenterRing from "./rings/CenterRing";

const Singularity = ({
  radius,
  tube,
  position,
  rotationSpeed,
  glowIntensity,
}) => {
  const ringRef = useRef();

  const glowTexture = useTexture("/images/glowtexture.png");

  const vertexShader = `
  varying vec2 vUv;

  void main() {
    vUv = uv;
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    gl_Position = projectionMatrix * mvPosition;
  }
`;

  const fragmentShader = `
  uniform sampler2D glowTexture;
  uniform vec3 color;
  uniform float intensity;

  varying vec2 vUv;

  void main() {
    vec4 texColor = texture2D(glowTexture, vUv);
    vec3 finalColor = color * texColor.rgb * intensity;
    gl_FragColor = vec4(finalColor, texColor.a);
  }
`;

  const glowMaterial = new ShaderMaterial({
    uniforms: {
      glowTexture: { value: glowTexture },
      color: { value: new THREE.Color("#7BFFFF") },
      intensity: { value: glowIntensity },
    },
    vertexShader: vertexShader,
    fragmentShader: fragmentShader,
    transparent: true,
    depthWrite: false,
  });

  useFrame((state, delta) => {
    ringRef.current && (ringRef.current.rotation.x += delta * rotationSpeed);
    ringRef.current && (ringRef.current.rotation.y += delta * rotationSpeed);
    ringRef.current && (ringRef.current.rotation.z += delta * rotationSpeed);
  });

  const geometry = useMemo(
    () => new THREE.TorusKnotGeometry(radius, tube, 300, 20, 10, 15),
    [radius, tube]
  );

  const material = useMemo(
    () =>
      new THREE.MeshStandardMaterial({
        color: "#00FFFF",
        emissive: "#00FFFF",
        emissiveIntensity: glowIntensity / 10,
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
      <sprite
        material={glowMaterial}
        position={[position[0], position[1], position[2] + 0.5]}
        scale={[radius * 15, radius * 15, radius * 15]} // Adjust the scale as needed
      />
    </>
  );
};

const OpticalCircle = (props) => {
  const { position, width, height, mouseRotate } = props;

  const [glowIntensity, setGlowIntensity] = useState(5);
  const [rotationSpeeds, setRotationSpeeds] = useState([
    0.05, 0.02, 0.1, 0.25, 0.5,
  ]);
  const isFirstRender = useRef(true);
  const groupRef = useRef();

  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      const initialSpeeds = rotationSpeeds.map((speed) => speed * 10);
      setRotationSpeeds(initialSpeeds);

      const transitionDuration = 5000; // 1000 ms = 1 second
      const startTime = performance.now();

      const animateTransition = () => {
        const elapsedTime = performance.now() - startTime;
        const progress = Math.min(elapsedTime / transitionDuration, 1);

        const newSpeeds = initialSpeeds.map((initialSpeed, index) => {
          const normalSpeed = initialSpeed / 10;
          return initialSpeed + (normalSpeed - initialSpeed) * progress;
        });

        setRotationSpeeds(newSpeeds);

        if (progress < 1) {
          requestAnimationFrame(animateTransition);
        }
      };

      requestAnimationFrame(animateTransition);
    }
  }, []);

  return (
    <div
      style={{
        position: position,
        width: width,
        height: height,
      }}
    >
      <Canvas>
        <ambientLight intensity={0.5} />
        <pointLight position={[0, 0, 10]} />
        <group ref={groupRef}>
          <UpperRing
            radius={1.75}
            tube={0.02}
            position={[0, 0, 1.25]}
            rotationSpeed={rotationSpeeds[0]}
            glowIntensity={glowIntensity}
          />
          <OuterRing
            radius={2.25}
            tube={0.0025}
            position={[0, 0, 0.75]}
            rotationSpeed={rotationSpeeds[1]}
            glowIntensity={glowIntensity}
          />
          <InnerRing
            radius={1.5}
            tube={0.02}
            position={[0, 0, -0.25]}
            rotationSpeed={rotationSpeeds[2]}
            glowIntensity={glowIntensity}
          />
          <CenterRing
            radius={1}
            tube={0.01}
            position={[0, 0, -1]}
            rotationSpeed={rotationSpeeds[3]}
            glowIntensity={glowIntensity}
          />
          <Singularity
            radius={0.25}
            tube={0.025}
            position={[0, 0, -1.25]}
            rotationSpeed={rotationSpeeds[4]}
            glowIntensity={glowIntensity}
          />
        </group>
        {mouseRotate && <OrbitControls enableZoom={false} enablePan={false} />}
      </Canvas>
    </div>
  );
};

export default OpticalCircle;
