import React from "react";
import { Container as ReactContainer} from "react-bootstrap";
import { ListGroup, Popover, OverlayTrigger, Badge } from 'react-bootstrap';
import userImage from "../images/user.png";
import logoImage from "../images/logo.png";
import LevelBadge from "./LevelBadge";

function Profile(props) {
    const { userFullName, userLevel, updateUserOptionsURL, logoutURL } = props;

    const levelBadge = <LevelBadge level={userLevel} />

    const UserPopover = (
        <Popover>
            <Popover.Title as="h3">
                {userFullName} {levelBadge}
            </Popover.Title>
                <ListGroup variant="flush">
                    <ListGroup.Item action href={updateUserOptionsURL}>
                        Options
                    </ListGroup.Item>
                    <ListGroup.Item action href={logoutURL}>
                        Logout
                    </ListGroup.Item>
                </ListGroup>
        </Popover>
    );

    return (
        <OverlayTrigger trigger="click" placement="bottom-end" overlay={UserPopover}>
            <img src={userImage} height="50px" />
        </OverlayTrigger>
    );
}

export default function Container(props) {
    const { userFullName, userLevel, updateUserOptionsURL, logoutURL } = props;

	return (
		<ReactContainer>
            <div style={{ display: "flex", justifyContent: "flex-start", position: "relative" }}>
                <img src={logoImage} style={{flex: "0 1 auto", position: "absolute", left: "50%", transform: "translateX(-50%)" }} height="50px" />
                <div style={{ flex: "0 1 auto", marginLeft: "auto" }}>
                    <Profile updateUserOptionsURL={updateUserOptionsURL} logoutURL={logoutURL} userFullName={userFullName} userLevel={userLevel} />
                </div>
            </div>
			{props.children}
		</ReactContainer>
	)
};