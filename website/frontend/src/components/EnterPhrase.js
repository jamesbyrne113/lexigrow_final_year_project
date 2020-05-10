import React, { useState, useRef } from "react";
import { Button, Col, FormControl, InputGroup, Row, Container } from 'react-bootstrap';


export default function EnterPhrase(props) {
	const [newPhrase, setNewPhrase] = useState("");
	const buttonRef = useRef(null);

	const keyPressed=(event)=> {
		if (event.key === "Enter") {
			buttonRef.current.click();
		}
	}

	const { selectTargetWordURL } = props;

	return (
		<Container>
			<Row>
				<Col>
					<InputGroup onKeyPress={e => keyPressed(e)}>
			 			<FormControl
							placeholder="Enter a phrase..."
							value={newPhrase}
							onChange={e => setNewPhrase(e.target.value)}
						/>
					</InputGroup>
				</Col>
				<Col md="auto">
					<Button ref={buttonRef} href={selectTargetWordURL + "?phrase=" + newPhrase}>Submit</Button>
				</Col>
			</Row>
		</Container>
	)
};