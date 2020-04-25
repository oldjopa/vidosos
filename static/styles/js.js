const vm = new Vue({
    el: '#app',
    data: {
        hasHours: false,
        id: ';',
        pl: false,
        ic: 'fas fa-play',
    },
    methods: {
        like() {
            axios.get('api/like').then(response => {
                this.id = response.data
            })
            alert(this.id)
        },
        play() {
            if (this.pl) {
                this.$refs.videoRef.pause()
                this.pl = false
                this.ic = 'fas fa-play'
            } else {
                this.$refs.videoRef.play()
                this.pl = true;
                this.ic = 'fas fa-pause'
            }

        },
        timeupdate() {
            this.$refs.currenttime.innerText = this.formatTime(this.$refs.videoRef.currentTime, this.hasHours);
            progress = Math.floor(this.$refs.videoRef.currentTime) / Math.floor(this.$refs.videoRef.duration);
            this.$refs.progress[0].style.width = Math.floor(progress * this.$refs.total.width()) + "px";
            console.log(this.$refs.progress[0].style.width)
            console.log(Math.floor(progress * this.$refs.total.width()) + "px")

        },

        can_play() {
            this.hasHours = (this.$refs.videoRef.duration / 3600) >= 1.0;
            console.log(this.formatTime(this.$refs.videoRef.duration, this.hasHours))
            this.$refs.duration.innerText = this.formatTime(this.$refs.videoRef.duration, this.hasHours);
            this.$refs.currenttime.innerText = this.formatTime(0, this.hasHours);
            console.log(this.formatTime(0, 0))
        },
        formatTime(time, hours) {
            if (hours) {
                h = Math.floor(time / 3600);
                time = time - h * 3600;

                m = Math.floor(time / 60);
                s = Math.floor(time % 60);

                return h.lead0(2) + ":" + m.lead0(2) + ":" + s.lead0(2);
            } else {
                m = Math.floor(time / 60);
                s = Math.floor(time % 60);

                return m.lead0(2) + ":" + s.lead0(2);
            }
        }

    },
});

Number.prototype.lead0 = function (n) {
    var nz = "" + this;
    while (nz.length < n) {
        nz = "0" + nz;
    }
    return nz
}