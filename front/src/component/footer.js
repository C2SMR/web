import React from "react";
import {button_click__dataLayer} from "../module/dataLayer";

export class Footer extends React.Component {
    render() {
        return (
            <footer>
                <h2>A bientôt!</h2>
                <img
                    style={{width: "50px", height: "50px"}}
                    src={"https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fstatic.vecteezy.com%2Fsystem%2Fresources%2Fpreviews%2F022%2F484%2F501%2Foriginal%2Fgoogle-play-store-icon-logo-symbol-free-png.png&f=1&nofb=1&ipt=ad7c8eeefe39aa2832952833b9ec1f055a59a75724599749109724d9ee7d0749&ipo=images"}
                    alt={"google play store"}
                    onClick={() => {
                        button_click__dataLayer("google play store");
                        window.open("https://play.google.com/store/apps/details?id=com.anonymous.C2SMR");
                    }}/>
            </footer>
        );
    }
}
