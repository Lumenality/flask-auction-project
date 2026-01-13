api_url = 'http://localhost:5000/api/v1/auctions';
const AuctionListCrudComponent = {
        delimiters: ["[[", "]]"],
        data() {
          return {
            auctions: [],
            message: "Hello Vue!",
          };
        },
        mounted() {
          this.fetchAuctions();
          console.log("Vue app mounted.");
        },
        methods: {
          fetchAuctions() {
            axios
              .get(api_url)
              .then((response) => {
                this.auctions = response.data;
                console.log("Auctions fetched:", this.auctions);
              })
              .catch((error) => {
                console.error("Error fetching auctions:", error);
              });
          },
        },
        template: /*html*/ `
        <div></div>
        `,
      };