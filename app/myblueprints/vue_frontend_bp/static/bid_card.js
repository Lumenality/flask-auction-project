const BidCardComponent = {
    delimiters: ["[[", "]]"],
    props: {
        bid: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            bidder:null,
        };
    },
    mounted() {
        this.fetchBidder();
    },
    methods: {
        fetchBidder() {
            axios
                .get(`/api/v1/users/${this.bid.user_id}`)
                .then((response) => {
                    this.bidder = response.data;
                    console.log("Bidder fetched:", this.bidder);
                })
                .catch((error) => {
                    console.error("Error fetching bidder:", error);
                });
        }
    },
    template: /*html*/ `
    <div class="card mb-2">
        <div class="card-body">
            <div v-if="bidder">
                <h4 class="card-title">Budgivare: [[ bidder.username ]]</h4>
                <a :href="'mailto:' + bidder.email">[[ bidder.email ]]</a>
            </div>
            <div v-else>
                <span>Laddar budgivarinformation...</span>
            </div>
            <p class="card-text">Bud ID: [[ bid.id ]]</p>
            <p class="h5 card-text">Summa: [[ bid.amount ]] kr.</p>
        </div>
    </div>
    `
};