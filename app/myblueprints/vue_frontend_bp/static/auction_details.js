const AuctionDetailsComponent = {
  delimiters: ["[[", "]]"],
  props: ["auctionId"],
  data() {
    return {
      auction: null,
      bids: [],
      loading: false,
      error: null,
      isAuthenticated: window.isAuthenticated === 'true' || window.isAuthenticated === true
    };
  },
  mounted() {
    this.fetchAuctionDetails();
    this.fetchBids();
    console.log("Auction details component mounted.");
  },
  methods: {
    fetchAuctionDetails() {
      this.loading = true;
      this.error = null;
      axios
        .get(`${api_url}/${this.auctionId}`)
        .then((response) => {
          this.auction = response.data;
          console.log("Auction details fetched:", this.auction, this.bids);
        })
        .catch((error) => {
          this.error = "Error fetching auction details: " + error.message;
          console.error("Error fetching auction details:", error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    fetchBids() {
      axios
        .get(`${api_url}/${this.auctionId}/bids`)
        .then((response) => {
          this.bids = response.data;
          console.log("Bids fetched:", this.bids);
        })
        .catch((error) => {
          console.error("Error fetching bids:", error);
        });
    },
    addBid(amount) {
      axios
        .post(`${api_url}/${this.auctionId}/bids`, { amount: amount })
        .then((response) => {
          this.bids.push(response.data);
          console.log("Bid added:", response.data);
        })
        .catch((error) => {
          console.error("Error adding bid:", error);
        });
    },
    likeAuction() {
      axios
        .post(`${api_url}/${this.auctionId}/like`)
        .then((response) => {
          if (this.auction) {
            this.auction.likes = response.data.likes;
            this.auction.dislikes = response.data.dislikes;
          }
        })
        .catch((error) => {
          console.error("Error liking auction:", error);
        });
    },
    dislikeAuction() {
      axios
        .post(`${api_url}/${this.auctionId}/dislike`)
        .then((response) => {
          if (this.auction) {
            this.auction.likes = response.data.likes;
            this.auction.dislikes = response.data.dislikes;
          }
        })
        .catch((error) => {
          console.error("Error disliking auction:", error);
        });
    },
  },
  template: /*html*/ `
    <div class="container mt-4" v-if="auction">
        <div class="row flex-lg-row-reverse align-items-center g-5 py-5">
            <div class="col-10 col-sm-8 col-lg-6">
                <img
                    :src="auction.image_url"
                    class="d-block mx-lg-auto img-fluid"
                    :alt="auction.description"
                    style="max-height: 500px"
                    loading="lazy"
                />
            </div>

            <div class="col-lg-6">
                <h1 class="display-5 fw-bold text-body-emphasis lh-1 mb-3">
                    [[ auction.description ]]
                </h1>

                <div class="d-flex flex-row mb-3">
                    <button
                        type="button"
                        @click="likeAuction"
                        class="thumb-counter d-flex flex-row align-items-center me-3 p-2 gap-1 text-success border-0 bg-transparent"
                    >
                        <p class="my-auto">[[ auction.likes ]]</p>
                        <i class="bi like-hands bi-hand-thumbs-up"></i>
                    </button>

                    <button
                        type="button"
                        @click="dislikeAuction"
                        class="thumb-counter d-flex flex-row align-items-center me-3 p-2 gap-1 text-danger border-0 bg-transparent"
                    >
                        <p class="my-auto">[[ auction.dislikes ]]</p>
                        <i class="bi like-hands bi-hand-thumbs-down"></i>
                    </button>
                </div>

                <p class="lead">
                    Starting Bid: $[[ auction.starting_bid ]]
                    <br />Duration: [[ auction.duration ]] days.
                </p>
            </div>
        </div>  
        <!-- Button trigger modal -->
        <button v-if="auction && isAuthenticated" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#bidModal">
        Add Bid
        </button>

        <div v-if="bids.length > 0">
            <h3>Top Bids:</h3>
            <div v-for="bid in bids" :key="bid.id" class="card mb-2">
                <div class="card-body">
                    <h5 class="card-title">Bidder: [[ bid.bidder_username ]]</h5>
                    <p class="card-text">Amount: $[[ bid.amount ]]</p>
                </div>
            </div>
        </div>


    <!-- Modal -->
    <div class="modal fade" id="bidModal" tabindex="-1" aria-labelledby="bidModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
        <div class="modal-header">
            <h1 class="modal-title fs-5" id="bidModalLabel">Add Bid</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
            ...
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary">Save changes</button>
        </div>
        </div>
    </div>
    </div>
    </div>
    `,
};
