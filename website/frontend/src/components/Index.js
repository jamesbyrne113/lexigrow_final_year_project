import React from "react";
import EnterPhrase from "./EnterPhrase";
import Container from "./Container";
import userImage from "../images/user.png";

export default function Index(props) {
    const { userFullName, userLevel, updateUserOptionsURL, logoutURL } = props;

	return (
		<Container updateUserOptionsURL={updateUserOptionsURL} logoutURL={logoutURL} userFullName={userFullName} userLevel={userLevel} >
			<div style={{"minHeight": "100%", "minHeight": "100vh", display: "flex", "alignItems": "center"}}>
				<EnterPhrase selectTargetWordURL={props.selectTargetWordURL} />
			</div>
		</Container>
	)
};