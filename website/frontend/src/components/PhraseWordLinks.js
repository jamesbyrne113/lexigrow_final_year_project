import React from "react";
import { Button, Container } from 'react-bootstrap';

export function PhraseWordLinks(props) {
    const { phraseInfoURL, phrase, phraseWords, startIndex } = props;
    
    return (
        <div>
            {phraseWords.map((word, index) => {
                return (
                    <Button 
                        href={phraseInfoURL + "?phrase=" + phrase + "&targetIndex=" + (startIndex + index)}
                        size="lg"
                        key={index} 
                        className='ml-1 mr-1 mb-4'
                        variant="info"
                    > 
                        {word}
                    </Button>
                );
            })}
        </div>
    )
}

export function TargetPhraseWordLinks(props) {
    const { phrase, hasTargetLinks, phraseInfoURL, targetIndex  } = props;

    var phraseWords = phrase.split(" ");
    
    return (
        <div>
            {phraseWords.map((word, index) => {
                if (hasTargetLinks[index]) {
                    return (
                        <Button 
                            variant={(index == targetIndex) ? "primary" : "link"}
                            size="lg"
                            key={index} 
                            className='ml-1 mr-1 mb-2 mt-2'
                            href={phraseInfoURL + "?phrase=" + phrase + "&targetIndex=" + index}
                        >
                            {word}
                        </Button>
                    );
                } else {
                    return (
                        <Button 
                            variant={(index == targetIndex) ? "primary" : ""}
                            size="lg"
                            key={index} 
                            className='ml-1 mr-1 mb-2 mt-2'
                        >
                            {word}
                        </Button>
                    );
                }
            })}
        </div>
    );
}
