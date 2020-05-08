import axios from 'axios';
import React, { useEffect, useState } from "react";
import { Alert, Col, Container, ListGroup, Row, Spinner, Tab, Tabs } from 'react-bootstrap';
import WordInfo from "./WordInfo";
import LevelBadge from "./LevelBadge";

const colours = ["success", "primary", "danger", "warning", "info"];

function Loading(props) {
	var spinnerColorIndex = Math.floor(Math.random() * colours.length);
	return (
		<Container style={{minWidth: "100%", height: "50vh", display: "flex", justifyContent: "center", alignItems: "center"}}>
			<Spinner animation="border" variant={colours[spinnerColorIndex]}>
				<span className="sr-only">Loading...</span>
			</Spinner>
		</Container>
	);
}

function NullContent(props) {
	return (
		<Container style={{minWidth: "100%", height: "50vh", display: "flex", justifyContent: "center", alignItems: "center"}}>
			<Alert>
				Sorry, there was an issue loading the {name} words
			</Alert>
		</Container>
	);
}

function RenderTab(props) {
	const [wordsInfo, setWordsInfo] = useState(null);
	const [loading, setLoading] = useState(true);

	const { name, wordsInfoURL, urlParams, selectTargetWordURL } = props;

	useEffect(() => {
		const fetchData = async () => {
			setLoading(true);
			axios.get(
				wordsInfoURL, {params: urlParams, responseType: 'json'}
			).then((response) => {
				setLoading(false);
				if (response.status == 200) {
					setWordsInfo(response.data.wordsInfo);
				} else {
					setWordsInfo(null);
				}
			}).catch((error) => {
				setLoading(false);
				setWordsInfo(null);
			});
		}

		fetchData();
	}, Object.keys(urlParams));

	if (loading) {
		return <Loading />
	} else if (wordsInfo == null) {
		return <NullContent />
	} else if (wordsInfo.length == 0) {
		return (
			<Alert>
				Sorry, We couldn't find any {name} words
			</Alert>
		)
	} else {
		return (
			<WordInfo wordsInfo={wordsInfo} selectTargetWordURL={selectTargetWordURL} />
		);
	}
}

function SameSound(props) {
	const [wordsInfo, setWordsInfo] = useState(null);
	const [loading, setLoading] = useState(true);

	const { wordsURL, urlParams } = props;

	useEffect(() => {
		const fetchData = async () => {
			setLoading(true);
			axios.get(
				wordsURL, {params: urlParams, responseType: 'json'}
			).then((response) => {
				setLoading(false);
				if (response.status == 200) {
					setWordsInfo(response.data.wordsInfo);
				} else {
					setWordsInfo(null);
				}
			}).catch((error) => {
				setLoading(false);
				setWordsInfo(null);
			});
		}

		fetchData();
	}, Object.keys(urlParams));

	const colours = ["success", "primary", "danger", "warning", "info"];

	if (loading) {
		return <Loading />
	} else if (wordsInfo == null) {
		return <NullContent />
	} else if (wordsInfo.length == 0) {
		return (
			<Alert>
				Sorry, We couldn't find any same sound words
			</Alert>
		)
	} else {
		return (
			<ListGroup variant="flush">
				{wordsInfo.map(wordInfo => {
					const levelBadge = <LevelBadge level={wordInfo.level} />
					return (
						<ListGroup.Item><h2>{levelBadge} : {wordInfo.word}</h2></ListGroup.Item>
					);
				})}  
        	</ListGroup>
		);
	}
}

export default function TabsMain(props) {
	const { similarContextInfoURL, similarMeaningInfoURL, similarMeaningWordNetInfo, sameSoundInfoURL, targetIndex, phrase, selectTargetWordURL } = props;

	const params = {
		targetIndex: targetIndex,
		phrase: phrase
	}

	return (
		<Container>
			<Row>
				<Col>
					<Tabs defaultActiveKey="context" id="similarWords">
						<Tab eventKey="context" title="Similar Context">
							<RenderTab wordsInfoURL={similarContextInfoURL} name="similar context" selectTargetWordURL={selectTargetWordURL} urlParams={params} />
						</Tab>
						{/* <Tab eventKey="meaning_word2vec" title="Similar Meaning Word2Vec">
							<RenderTab wordsInfoURL={similarMeaningInfoURL} name="similar meaning Word2Vec" selectTargetWordURL={selectTargetWordURL} urlParams={params} />
						</Tab> */}
						<Tab eventKey="meaning_wordnet" title="Similar Meaning WordNet">
							<RenderTab wordsInfoURL={similarMeaningWordNetInfo} name="similar meaning WordNet" selectTargetWordURL={selectTargetWordURL} urlParams={params} />
						</Tab>
						<Tab eventKey="sound" title="Same Sound">
							<SameSound wordsURL={sameSoundInfoURL} urlParams={params} />
						</Tab>
					</Tabs>
				</Col>
			</Row>
		</Container>
	);
}