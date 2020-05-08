import React from "react";
import { Badge } from 'react-bootstrap';

const levelColors = {
    "A1": "success",
    "A2": "info",
    "B1": "primary",
    "B2": "warning",
    "C": "danger",
    "C1": "danger",
    "C2": "danger"
};
// const letterLevel = ["A1", "A2", "B1", "B2", "C"];

export default function LevelBadge(props) {
    const { level } = props;

    if (level == null) {
       return (
            <Badge variant="dark">Unknown</Badge>
       )
    } else {
        return (
            <Badge variant={levelColors[level]}>{level}</Badge>
        )
    }
};