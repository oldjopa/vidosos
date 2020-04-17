new Vue({
    el: '#app',
    data: {
        src: "/vidosos/static/video/first.mp4",
        id: null
    },
    methods: {
        like() {
            axios
                .get('localhost/api/current')
                .then(response => (this.id = responce))
                .post('localhost/api/like/' + id)
                .catch(error => console.log(error));
        }
    }
});

document.querySelector('#play').onclick = play;

let video;
var pl = false;

video = document.querySelector('#video-player');

function play() {
    if (pl) {
        video.pause();
        pl = false;
    } else {
        video.play();
        pl = true;
    }

}