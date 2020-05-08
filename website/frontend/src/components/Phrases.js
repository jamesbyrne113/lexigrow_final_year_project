import React from "react";
import { Alert, Container, Row, Col } from 'react-bootstrap';

function getExamples(examples, selectTargetWordURL) {
    if (examples.length == 0) {
        return <Alert variant="secondary">Sorry, there are no examples currently available for this word</Alert>
    } else {
        return (<ul>
            {examples.map(example => {
                return (
                    <li key={example}>
                        <a href={selectTargetWordURL + "?phrase=" + example}>{example}</a>
                    </li>
                );
            })}
        </ul>);
    }
}

function getDefinition (definition) {
    if (definition) {
        return (<h4>{definition}</h4>);
    } else {
        return (
            <Alert variant="secondary">Sorry, there is no definition currently available for this word</Alert>
        )
    }
}

export default function Phrases(props) {
    const {  details, selectTargetWordURL } = props;

    if (details.length == 0) {
        return (
            <Alert variant="secondary">Sorry, there is no information currently available about this word</Alert>
        );
    }

	return (
        <Container>
            {details.map(detail => 
                <Row key={detail.definition}>
                    <Col>
                        {getDefinition(detail.definition)}
                        {getExamples(detail.examples, selectTargetWordURL)}
                    </Col>
                </Row>
            )}
        </Container>
    );
};