const AuctionDetailsComponent = {
  delimiters: ["[[", "]]"],
  props: ["auctionId"],
  data() {
    return {
      auction: null,
      bids: [],
      loading: false,
      error: null,
      end_time_formatted: null,
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
        .get(`${auctions_api_url}/${this.auctionId}`)
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
        .get(`${auctions_api_url}/${this.auctionId}/bids`)
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
        .post(`${auctions_api_url}/${this.auctionId}/bids`, { amount: amount })
        .then((response) => {
          this.bids.push(response.data);
          location.reload();
          console.log("Bid added:", response.data);
        })
        .catch((error) => {
          console.error("Error adding bid:", error);
        });
    },
    likeAuction() {
      axios
        .post(`${auctions_api_url}/${this.auctionId}/like`)
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
        .post(`${auctions_api_url}/${this.auctionId}/dislike`)
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
    formatDate() {
        if (this.auction && this.auction.end_time) {
            const options = { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' };
            const date = new Date(this.auction.end_time);
            return date.toLocaleDateString('sv-SE', options).replace(',', '');
        }
    }
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
                <span class="text-black-50" style="font-size: 1rem">[[ formatDate() ]]</span>
                <like-dislike-buttons
                  :auction-id="auction.id"
                  :likes="auction.likes"
                  :dislikes="auction.dislikes"
                  @like-auction="likeAuction"
                  @dislike-auction="dislikeAuction"
                ></like-dislike-buttons>

                <p class="lead">
                    Start bud: [[ auction.starting_bid ]] kr.<br>
                    Högsta bud: [[ auction.highest_bid ]] kr.<br />
                </p>
            </div>
        </div>  
        <!-- Button trigger modal -->


      <div v-if="bids.length > 0">
        <div class="d-flex flex-row align-items-center gap-3">
        <h3 class="mb-0">Top Bids:</h3>
        <button v-if="auction && isAuthenticated" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#bidModal">
          Add Bid
        </button>
        </div>
        <div class="mt-3">
          <bid-card-component v-for="bid in bids" :key="bid.id" :bid="bid"></bid-card-component>
        </div>
      </div>
      <div v-else>
        <h3 class="h4 text-muted">No bids yet. Be the first to bid!</h3>
        <button v-if="auction && isAuthenticated" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#bidModal">
          Add Bid
        </button>
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
            <form @submit.prevent="addBid($event.target.bidAmount.value)">
            <div class="mb-3">
                <label for="bidAmount" class="form-label">Bid Amount</label>
                <input type="number" class="form-control" id="bidAmount" name="bidAmount" :value="auction.highest_bid + 1" required :min="auction.highest_bid + 1" step="1">
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="submit" class="btn btn-primary">Submit Bid</button>
            </div>
            </form>
        </div>

        </div>
    </div>
    </div>
    </div>
    `,
};
