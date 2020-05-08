import React from "react";
import { Container } from 'react-bootstrap';
import LevelBadge from "./LevelBadge";
import Phrases from "./Phrases";

export default function WordInfo(props) {
    const { wordsInfo, selectTargetWordURL } = props;

    debugger;

    return (
        <Container>
            {wordsInfo.map(wordInfo => {
                const { level, word, pos, details } = wordInfo;
                const levelBadge = <LevelBadge level={level} />

                return (
                    <div key={word + pos}>
                        <h2>{levelBadge} {word} : {pos}</h2>
                        <Phrases details={details} selectTargetWordURL={selectTargetWordURL} />
                    </div>
                );
            })}  
        </Container>
    );
};