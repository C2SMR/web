import React from "react";
import Moveable from "react-moveable";

export class Zone extends React.Component {

    constructor(props) {
        super(props);
        this.url = "https://api.c2smr.fr/"
        this.name = new URLSearchParams(document.location.search).get("name");
        this.key = new URLSearchParams(document.location.search).get("key");
        this.get_image().then(r => console.log(r));
        this.fetch_zone().then(r => console.log(r));
        this.state = {
            zone: [],
            image: "",
            last_zone_id: 0
        };
    }

    async get_image() {
        let image = await fetch(this.url + "client/get_picture", {
            method: "POST",
            body: JSON.stringify({
                "city": this.name + '.png',
            })
        });
        console.log('************')
        console.log(image);
        image = await image.json();
        console.log(image);
        image = image.picture;
        this.setState({image: image});
    }

    async fetch_zone() {
        let zone = await fetch(this.url + "zone?city=" + this.name);
        zone = await zone.json();
        zone = zone.data;
        this.setState({zone: zone});
    }

    async add_zone(type, x, y, width, height) {
        await fetch(this.url + "zone", {
            method: "POST",
            body: JSON.stringify({
                "city": this.name,
                "key": this.key,
                "type": type,
                "x1": x,
                "x2": y,
                "y1": width,
                "y2": height
            })
        })
        await this.fetch_zone();
    }

    async delete_zone() {
        await fetch(this.url + "zone", {
            method: "DELETE",
            body: JSON.stringify({
                "id": this.state.last_zone_id,
                "key": this.key
            })
        })
        await this.fetch_zone();
    }

    async modify_zone() {
        this.state.zone.map(async (z, index) => {
            await fetch(this.url + "zone", {
                method: "PUT",
                body: JSON.stringify({
                    "id": z[0],
                    "key": this.key,
                    "type": z[1],
                    "x1": z[2],
                    "x2": z[3],
                    "y1": z[4],
                    "y2": z[5]
                })
            })
        });
        await this.fetch_zone();
    }


    render() {
        return (
            <div class={"container-zone"}>
                <img src={'data:image/png;base64,' + this.state.image} alt={"background"}/>
                <div>
                    <button onClick={() => this.add_zone(0, 0, 0, 0, 0)}>Add zone type 1</button>
                    <button onClick={() => this.add_zone(1, 0, 0, 0, 0)}>Add zone type 2</button>
                    <button onClick={() => this.add_zone(2, 0, 0, 0, 0)}>Add zone type 3</button>
                </div>
                <div>
                    <button onClick={() => this.delete_zone(0)}>Delete zone</button>
                </div>
                <div>
                    <button onClick={() => this.modify_zone()}>SAVE</button>
                </div>
                {
                    this.state.zone.map((z, index) => <div className={"target"}
                                                           style={{
                                                               left: z[2],
                                                               top: z[3],
                                                               width: z[4],
                                                               height: z[5],
                                                           }}
                                                           id={"zone" + index.toString()}>{z[1]}</div>)
                }
                {
                    this.state.zone.map((z, index) => <Moveable
                        target={document.querySelector("#zone" + index.toString())}
                        draggable={true}
                        resizable={true}
                        onDrag={({
                                     target,
                                     beforeDelta, beforeDist,
                                     left, top,
                                     right, bottom,
                                     delta, dist,
                                     transform,
                                     clientX, clientY,
                                 }) => {
                            target.style.left = `${left}px`;
                            target.style.top = `${top}px`;
                            this.setState({last_zone_id: this.state.zone[index][0]});
                            const temp_zone = this.state.zone;
                            temp_zone[index][2] = left;
                            temp_zone[index][3] = top;
                            this.setState({zone: temp_zone});
                        }}
                        onResize={({
                                       target, width, height,
                                       dist, delta, direction,
                                       clientX, clientY,
                                   }) => {
                            delta[0] && (target.style.width = `${width}px`);
                            delta[1] && (target.style.height = `${height}px`);
                            this.setState({last_zone_id: this.state.zone[index][0]});
                            const temp_zone = this.state.zone;
                            temp_zone[index][4] = width;
                            temp_zone[index][5] = height;
                            this.setState({zone: temp_zone});
                        }}
                    />)
                }
            </div>
        );
    }
}