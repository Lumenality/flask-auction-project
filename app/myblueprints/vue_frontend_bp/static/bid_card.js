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
        }, 
        formatDate() {
        if (this.bid && this.bid.created_at) {
            const options = { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' };
            const date = new Date(this.bid.created_at);
            return date.toLocaleDateString('sv-SE', options).replace(',', '');
        }
    }
    },
    template: /*html*/ `
    <div class="card mb-2">
        <div class="card-body">
            <div class="d-flex justify-content-between w-100 mb-2">
                <p class="card-text text-black-50 mb-0" style="font-size: 0.9em;">Budets tidpunkt: [[ formatDate() ]]</p>
                <p class="card-text text-black-50 mb-0" style="font-size: 0.9em;">Bud ID: [[ bid.id ]]</p>
            </div>
            <div v-if="bidder">
                <h6 class="card-title">[[ bidder.username ]] | <a :href="'mailto:' + bidder.email">[[ bidder.email ]]</a> </h6>
                
            </div>
            <div v-else>
                <span>Laddar budgivarinformation...</span>
            </div>
            
            <p class="display-6 card-text">[[ bid.amount ]] kr.</p>
        </div>
    </div>
    `
};