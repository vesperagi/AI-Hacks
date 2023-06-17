"use client";

import { useState } from "react";

import { Button, Flex, Input } from "@chakra-ui/react";

import OpticalCircle from "@/Valara/OpticalCircle";

// BACKEND IMPORTS

import { firestore } from "@/utils/firebase";

const sampleChat = [{ member }];

export default function Home() {
  const [input, setInput] = useState("");

  return (
    <Flex
      flexDirection={"column"}
      justifyContent={"center"}
      alignItems={"center"}
      w={"100vw"}
      h={"100vh"}
      bgColor={"#000000"}
    >
      {/* <OpticalCircle position={"relative"} width={"300px"} height={"300px"} /> */}

      {/** CHAT */}

      <Flex flexDirection={"column"} alignItems={"center"}></Flex>

      {/** INPUT */}

      <form>
        <Flex flexDirection={"row"} alignItems={"center"} gap={"5px"}>
          <Input
            value={prompt}
            placeholder={"talk to valara!"}
            bgColor={"#FFFFFF"}
            onChange={(e) => setPrompt(e.target.value)}
          />
          <Button type={"submit"}>Enter</Button>
        </Flex>
      </form>
    </Flex>
  );
}

