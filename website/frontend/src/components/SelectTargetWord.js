import React from "react";
import { Alert } from 'react-bootstrap';
import EnterPhrase from "./EnterPhrase";
import { PhraseWordLinks } from "./PhraseWordLinks";
import { TargetPhraseWordLinks } from "./PhraseWordLinks";
import Container from './Container';

export default function SelectTargetWord(props) {
    const {
        userFullName,
        userLevel,
		updateUserOptionsURL, 
        logoutURL,
        selectTargetWordURL,
        hasTargetLinks,
        phraseInfoURL,
        phrase
    } = props;
    
	return (
		<Container updateUserOptionsURL={updateUserOptionsURL} logoutURL={logoutURL} userFullName={userFullName} userLevel={userLevel} >
            <div style={{"minHeight": "100%", "minHeight": "100vh", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center"}}>
                <PhraseWordLinks hasTargetLinks={hasTargetLinks} phraseInfoURL={phraseInfoURL} phrase={phrase} phraseWords={phrase.split(" ")} startIndex={0} />

                <Alert
                    style={{
                        textAlign: "center",
                    }}
                    variant="light"
                >
                    Select a word above for more information or enter in a different phrase
                </Alert>

                <EnterPhrase selectTargetWordURL={selectTargetWordURL} />
            </div>
		</Container>
	)
};