import React from "react";

export class View extends React.Component {

    constructor(props) {
        super(props);
        this.url = "https://api.c2smr.fr/"
        this.name = new URLSearchParams(document.location.search).get("name");
        setInterval(() => this.get_image(), 1000);
        this.state = {
            image: null,
        }
    }

    async get_image() {
        let image = await fetch(this.url + "client/get_picture", {
            method: "POST",
            body: JSON.stringify({
                "city": this.name + '.png',
            })
        });
        image = await image.json();
        image = image.picture;
        this.setState({image: image});
    }


    render() {
        return (
            <div class={"container-zone"}>
                <img src={'data:image/png;base64,' + this.state.image} alt={"background"}/>
            </div>
        );
    }
}