import React from "react";
import 'babel-polyfill';
import { render } from "react-dom";
import PhraseInfo from "./PhraseInfo";
import Index from "./Index";
import SelectTargetWord from "./SelectTargetWord";

const container = document.getElementById("app");

switch (window.pageName.toLowerCase()) {
	case "phrase_info":
		render(<PhraseInfo {...window.context}/>, container);
		break;

	case "select_target_word":
		render(<SelectTargetWord {...window.context}/>, container)
		break;

	default:
		render(<Index {...window.context} />, container);
		break;
}