import React, { useState } from "react";
import { Row, Toast } from 'react-bootstrap';
import Container from './Container';
import EnterPhrase from "./EnterPhrase";
import { TargetPhraseWordLinks } from "./PhraseWordLinks";
import TabsMain from "./TabsMain";
import WordInfo from "./WordInfo";

function SeenWordToast(props) {
	const {word, poses } = props;

	const [show, setShow] = useState(true);

	return (
		<Toast onClose={() => setShow(false)} show={show} delay={6000} autohide style={{ position: 'absolute', top: 0, right: 0 }}>
			<Toast.Header><h3>{word}</h3></Toast.Header>
			<Toast.Body>Good Job! You have used the word <span style={{fontWeight: "bold"}}>{word}</span> you have seen previously as a {poses}</Toast.Body>
		</Toast>
	  );
}

function SeenWordsToasts(props) {
	const {seenWords} = props;

	return (
		<div>
			{Object.keys(seenWords).map(word => <SeenWordToast word={word} poses={seenWords[word]} />)}
		</div>
	)
}


export default function PhraseInfo(props) {
	const { 
		userFullName,
		userLevel,
		updateUserOptionsURL, 
		logoutURL,
		phrase, 
		hasTargetLinks, 
		targetWordsInfo, 
		selectTargetWordURL, 
		similarContextInfoURL, 
		similarMeaningInfoURL, 
		similarMeaningWordNetInfo, 
		sameSoundInfoURL, 
		phraseInfoURL,
		targetIndex,
		seenWords
	} = props;

	return (
		<Container updateUserOptionsURL={updateUserOptionsURL} logoutURL={logoutURL} userFullName={userFullName} userLevel={userLevel} >
			<Row>
				<div style={{minWidth: "100%", display: "flex", justifyContent: "center"}}>
					<TargetPhraseWordLinks 
						phrase={phrase}
						hasTargetLinks={hasTargetLinks}
						targetIndex={targetIndex} 
						phraseInfoURL={phraseInfoURL} 
					/>
				</div>
			</Row>
			<div style={{minWidth: "100%", display: "flex", justifyContent: "center" }}>
				<div style={{display: "flex", flex: 1}}>
					<WordInfo 
						wordsInfo={targetWordsInfo} 
						selectTargetWordURL={selectTargetWordURL}
					/>
				</div>
				<img src={"https://source.unsplash.com/featured?" + targetWordsInfo[0].word + "/800x600"} width="300" height="225"/>
			</div>
			<TabsMain 
				targetWordsInfo={targetWordsInfo}
				similarContextInfoURL={similarContextInfoURL}
				similarMeaningInfoURL={similarMeaningInfoURL}
				similarMeaningWordNetInfo={similarMeaningWordNetInfo} 
				sameSoundInfoURL={sameSoundInfoURL} 
				selectTargetWordURL={selectTargetWordURL}
				targetIndex={targetIndex} 
				phrase={phrase} 
			/>
			<Row>
				<EnterPhrase selectTargetWordURL={selectTargetWordURL}/>
			</Row>
			<SeenWordsToasts seenWords={seenWords} />
		</Container>
	)
};